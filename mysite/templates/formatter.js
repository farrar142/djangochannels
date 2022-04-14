var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const marketid = "1";

const test_url = ws_scheme + "://ws.honeycombpizza.link/ws/notify/";
const url =
  ws_scheme + "://" + window.location.host + "/ws/price/" + marketid + "/";
const home_url =
  ws_scheme + "://" + window.location.host + "/ws/price/" + marketid + "/";
const personal =
  ws_scheme +
  "://" +
  window.location.host +
  "/ws/personal/" +
  btoa("0eade8a4-24d1-47fd-a231-7cef784ed326") +
  "/";
function connect() {
  var chatSocket = new WebSocket(test_url);

  chatSocket.onopen = function (e) {
    console.log(e);
    console.log(chatSocket);
    console.log(e.timeStamp);
  };
  chatSocket.onmessage = function (e) {
    console.log(e);
    console.log(e.data);
    console.log(JSON.parse(e.data));
    datas = JSON.parse(e.data)["datas"];
    let context = "";
    for (key in datas) {
      let data = datas[key];
      context =
        context +
        context_stacker(
          data["trade_order_id"],
          data["product_name"],
          data["user_name"],
          data["type_name"],
          data["reg_amount"],
          data["cur_amount"],
          data["reg_date"],
          data["code_id"]
        );
    }
    renderer(context);
  };
  chatSocket.onclose = function (e) {
    console.log(
      "Socket is closed. Reconnect will be attempted in 1 second.",
      e.reason
    );
    setTimeout(function () {
      connect();
    }, 1000);
  };

  chatSocket.onerror = function (err) {
    console.error("Socket encountered error: ", err.message, "Closing socket");
    chatSocket.close();
  };
}

connect();

function context_stacker(
  번호,
  업체,
  유저이름,
  타입,
  목표거래량,
  남은거래량,
  일시,
  상태
) {
  if (상태 == 4) {
    상태 = "HOLD";
  } else if (상태 == 5) {
    상태 = "MARKET";
  } else {
    상태 = "CANCELED";
  }
  return `
    <div>거래번호 : ${번호},업체 : ${업체}, 거래자 : ${유저이름}, 유형 : ${타입}, 상태 : ${상태}, 목표거래량 : ${목표거래량}, 남은거래량 ${남은거래량}, 일시 : ${일시}  </div>

    `;
}
function renderer(context) {
  $("#목록").html(context);
}
