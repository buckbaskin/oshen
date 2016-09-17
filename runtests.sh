export STATUS=TESTING
echo $STATUS
nosetests \
--with-timer --timer-top-n 5 --timer-ok 250ms --timer-warning 500ms \
--with-coverage --cover-erase --cover-html --cover-package=app --cover-branches \
apiserver/tests/

result=$?
export STATUS=Production
if [ $result != 0 ]; then
    echo $result
    exit 1
else
    codecov
    exit 0
fi
