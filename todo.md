[o]1. 현재는 장고 orm에서 쿼리해와서 기존 거래 기록을 뿌려줌.
[o]2. 이를 웹소켓에 접속!(accept)할때 ,거래가 성사(receive)될때! 쿼리하도록 바꿀예정.

[]3. 에셋-트레이드 간의 로직, 거래로직 필요
###구매하는 쪽은 판매쪽의 가장오래된 regdate를 가지는 trade에서 quantity를 차감후  asset으로 전환
###판매하는 쪽은 자신의 asset을 trade로 전환
#market.models.Trade.trade_logic 수정요

[]4. 프론트/백엔드 로그인구현

[]5. 스케쥴러를 이용해 Product를 ProductLog로 migrate