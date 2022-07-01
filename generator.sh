#!/bin/bash
#pkill -f otree
#rm -rf db.sqli*
#od &
#pid=$!
#sleep 5
#kill $pid
otree mocking_data baseline 1 &&
otree mocking_data fin 1 &&
otree mocking_data gamified 1 &&
otree mocking_data full 1 &&
od


