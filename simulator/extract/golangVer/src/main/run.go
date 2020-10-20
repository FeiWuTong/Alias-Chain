package main

import (
	"fmt"
	"strconv"
	"time"

	"addrdb"
	"common"
)

func newTestIDDB(dbpath string) (*addrdb.IDDatabase, func()) {
	db, err := addrdb.NewIDDatabase(dbpath)
	if err != nil {
		panic("failed to open test database: " + err.Error())
	}

	return db, func() {
		db.Close()
		//os.RemoveAll(db.Get_path())
	}
}

// flag: 0 -> start, 1 -> end
func Evaluate(flag bool, start *int64) {
	if flag {
		fmt.Printf("Finish with time cost: %v seconds\n", float64(time.Now().UnixNano()-*start)/1E9)
	} else {
		*start = time.Now().UnixNano()
	}
}

func main() {
	// Addr -> To, AddrF -> From, AddrTest -> Test (Database)
	// Alter here
	dbpath := "./AddrDatabase5"
	filepathTo := "./InputData/ToStatis"
	filepathFrom := "./InputData/FromStatis"
	output_path_T := "./OutputData/DBToOutput4"
	output_path_F := "./OutputData/DBFTOutput4"
	var start int64
	reading := true
	traverse := true

	db, remove := newTestIDDB(dbpath)
	defer remove()

	if reading {
		fmt.Println("Start reading and recording...")
		// Alter i
		for i := 31; i <= 40; i++ {
			fmt.Printf("Now processing ToStatis%d...\n", i)
			Evaluate(false, &start)
			common.ReadLine(db, filepathTo+strconv.Itoa(i), common.DBRecord)
			Evaluate(true, &start)
		}
		if traverse {
			Evaluate(false, &start)
			common.TraverseDB(db, output_path_T)
			Evaluate(true, &start)
		}
		for i := 31; i <= 40; i++ {
			fmt.Printf("Now processing FromStatis%d...\n", i)
			Evaluate(false, &start)
			common.ReadLine(db, filepathFrom+strconv.Itoa(i), common.DBRecord)
			Evaluate(true, &start)
		}
		if traverse {
			Evaluate(false, &start)
			common.TraverseDB(db, output_path_F)
			Evaluate(true, &start)
		}
	}
	/*
		if traverse {
			Evaluate(false, &start)
			common.TraverseDB(db)
			Evaluate(true, &start)
		}
	*/
}
