xcopy ".\..\..\timed_producer.py" "." /Y /F
xcopy ".\..\..\consumer.py" "." /Y /F
docker build -f python.Dockerfile -t rabbit-flow .
