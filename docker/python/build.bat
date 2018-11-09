xcopy ".\..\..\timed_producer.py" "." /Y /F
xcopy ".\..\..\consumer.py" "." /Y /F
xcopy ".\..\..\api.py" "." /Y /F
xcopy ".\..\..\worker.py" "." /Y /F
docker build -f Dockerfile -t rabbit-flow .
