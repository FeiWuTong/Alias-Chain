package common

import (
	"bufio"
	"log"
	"os"
	"strconv"

	//"fmt"

	"addrdb"
)

func ReadLine(db *addrdb.IDDatabase, fp string, hookfn func(*addrdb.IDDatabase, []byte)) {
	f, err := os.Open(fp)
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err = f.Close(); err != nil {
			log.Fatal(err)
		}
	}()
	bfSc := bufio.NewScanner(f)
	for bfSc.Scan() {
		hookfn(db, bfSc.Bytes())
	}
	if err = bfSc.Err(); err != nil {
		log.Fatal(err)
	}
}

func DBRecord(db *addrdb.IDDatabase, key []byte) {
	value, err := db.Get(key)
	if value == nil {
		if err = db.Put(key, []byte("1")); err != nil {
			log.Fatal(err)
		}
	} else {
		value_int, err := strconv.Atoi(string(value))
		value_int += 1
		if err = db.Put(key, []byte(strconv.Itoa(value_int))); err != nil {
			log.Fatal(err)
		}
	}
}

func ProceedTest(db *addrdb.IDDatabase, content []byte) {
	os.Stdout.Write(content)
}

func TraverseDB(db *addrdb.IDDatabase, fp string) {
	iter := db.NewIterator()
	//file_row := 2500000
	//acc := 0
	content := make(chan string, 100)
	exit := make(chan bool)
	// alter here
	//output_path := "./OutputData/DBToOutput_"

	go func() {
		for iter.Next() {
			content <- (string(iter.Key()) + " " + string(iter.Value()) + "\n")
		}
		close(content)
	}()

	go func() {
		//file_num := 1
		for {
			//f, err := os.OpenFile(output_path+strconv.Itoa(file_num), os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
			f, err := os.OpenFile(fp, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
			if err != nil {
				log.Fatal(err)
			}
			w := bufio.NewWriter(f)
			for {
				v, ok := <-content
				if ok {
					//acc++
					w.WriteString(v)
				} else {
					w.Flush()
					f.Close()
					exit <- true
					return
				}
				/* only 1 file
				if acc == file_row {
					file_num++
					acc = 0
					w.Flush()
					f.Close()
					break
				}
				*/
			}
		}
	}()

	<-exit
	iter.Release()
	if err := iter.Error(); err != nil {
		log.Fatal(err)
	}

	/*
		iter := db.NewIterator()
		f, err := os.OpenFile("./OutputData/DBOutput", os.O_WRONLY | os.O_CREATE | os.O_APPEND, 0666)
		if err != nil {
			log.Fatal(err)
		}
		defer f.Close()
		w := bufio.NewWriter(f)
		for iter.Next() {
			//fmt.Printf("[%s]: %s\n", iter.Key(), iter.Value())
			w.WriteString(string(iter.Key()) + " " + string(iter.Value()) + "\n")
		}
		w.Flush()
		iter.Release()
		if err := iter.Error(); err != nil {
			log.Fatal(err)
		}
	*/
}
