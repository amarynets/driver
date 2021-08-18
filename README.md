To run project need to do following:
1. Create `.env` file near docker-compose
2. Fill this file from `.env.example` and change value on demand
3. Run command `docker-compose up`
4. If you want to change time interval or number of drivers - you have to change `.env` and restart `generator` service: `docker-compose restart generator`

Docs available by link: http://127.0.0.1:8000/docs