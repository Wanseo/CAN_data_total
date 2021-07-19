WRITER : WANSEOJO / DATE : 21-7-20 / TITLE : _ME, _RADAR FILES TO TOTAL.CSV FILE

ENG 
# << READ ME >>

* The following code combines the _me.csv or _radar.csv data file, which is CAN data, and converts it into one intergrated _total.csv     file.
* Starting with rootdir, one integrated _total.csv file is created according to the selected file (_me, _radar) for each dir folder.
* Errors found in the process of converting to an integrated file (please refer to << ERROR HANDLING >> part. ) are collected from all   dir's error logs and generated from root dir as one error_log.txt file.

# << ERROR HANDLING >>

The types of errors recorded as error_log.txt are as follows.
* Num of files Error : _me.csv != 11 or, _radar.csv != 19 -> ERROR !
* Time Stamp Error : Check time stamp for each file if float value is different -> ERROR!
* Row Nan value Error: If row does not have a value (if Nan) -> Error!

# << DATA >>

* _me.csv :  _me, _me1, ... _me10
* _radar.csv : _radar, _radar1, ... _me18
* and others ..

KOR 
# << READ ME >>

* 다음의 코드는 CAN data 인 _me.csv or _radar.csv 데이터 파일을 합쳐 각각 하나의 통합된 csv 파일로 변환시켜주는 코드입니다.
* root dir 에서 시작해 모든 dir 폴더마다 선택된 파일 (_me, _radar) 에 따른 하나의 통합된 _total.csv 파일이 만들어집니다.
* 통합파일로 변환하는 과정에서 발견되는 error는 ( << ERROR HANDLING >> 참고! ) 모든 dir 의 에러 로그가 모아져 root dir 에서 하나의 error_log.txt 파일로 생성됩니다.

# << ERROR HANDLING >>

* error_log.txt 로 기록되는 에러의 종류는 다음과 같습니다.
* Num of files Error : _me.csv != 11 개 or _radar.csv != 19 개  -> ERROR ! 
* Time Stamp Error : 파일마다 time stamp 를 체크해 float 값이 다른 경우 -> ERROR !
* Row Nan value Error : row 에 값이 없는 경우 (Nan 인 경우 ) -> Error !

# << DATA >> 

* _me.csv : _me, _me1, ... _me10
* _radar.csv : _radar, _radar1, ... _me18
* 그리고, 그 외의 것들..
    
