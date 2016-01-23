{
    if (FNR>1) {
	
	# --- Get type
        d=substr($1,0,1);
	if (d=="\x00") { d=substr($1,1,1); }

	# --- Get size
        s=$3; 

	# --- Display
        $1=$2=$3=$4=$5=$6="";
        gsub(/^[ ]+/, "", $0);
    	print d,s,substr($0,0,256);
    }
}
