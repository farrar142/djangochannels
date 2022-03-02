docker restart daphne && docker logs --tail 10 -f daphne
docker rm -f blog&& docker-compose up
docker exec -it daphne bash

python3 manage.py runserver 0.0.0.0:8021

https://americanopeople.tistory.com/category/%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4-%EC%9D%B4%EC%95%BC%EA%B8%B0/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4%EC%99%80%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete


[mariadb]
show variables where Variable_name in 'general_log';
show variables like 'general%';
set global general_log=ON;


python3 manage.py graph_models -a -I User,Wallet,Point,Point_History,Asset_Item,AsyncModel,Type,Code,Event,Product_Category,Product,ProductLog,Trade_Order,Buyer,Seller -o my_project.png

python3 manage.py graph_models -a -I User,Wallet,Point,Point_History,Asset_Item,AsyncModel,Type,Code,Event,Product_Category,Product,ProductLog,Trade_Order,Buyer,Seller -o my_project.png --pygraphviz

pip install pygraphviz 안될때.
apt-get install python-dev graphviz libgraphviz-dev pkg-config