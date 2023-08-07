if ! hash python3; then
    echo "python is not installed"
    exit 1
fi
if ! hash pip3; then 
	echo "pip is not intsalled"
	exit 1
fi
ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "31" ]; then
	echo $ver
    echo "This script requires python 3.10 or greater"
    exit 1
else 
	pip3 install virtualenv 
	python3 -m venv CamFitzpatrickvenv

	for package in $(ls ./dependencies)
	do 
		echo $package
		./CamFitzpatrickvenv/bin/pip3 install ./dependencies/$package
	done 	
fi

