package addrdb

import (
	"github.com/syndtr/goleveldb/leveldb"
	"github.com/syndtr/goleveldb/leveldb/iterator"
)

type IDDatabase struct {
	db_path string
	db *leveldb.DB
}

func NewIDDatabase(dirname string) (*IDDatabase, error) {
	db_path := dirname
	db, err := leveldb.OpenFile(db_path, nil)
	if err != nil {
		return nil, err
	}
	return &IDDatabase{
		db_path:	db_path,
		db:			db,
	}, nil
}

func (db *IDDatabase) Get_path() string {
	return db.db_path
}

func (db *IDDatabase) IDDB() *leveldb.DB {
	return db.db
}

func (db *IDDatabase) Put(key []byte, value []byte) error {
	return db.db.Put(key, value, nil)
}

func (db *IDDatabase) Get(key []byte) ([]byte, error) {
	dat, err := db.db.Get(key, nil)
	if err != nil {
		return nil, err
	}
	return dat, nil
}

func (db *IDDatabase) Delete(key []byte) (error) {
	return db.db.Delete(key, nil)
}

func (db *IDDatabase) Close() {
	db.db.Close()
}

func (db *IDDatabase) NewIterator() iterator.Iterator {
	return db.db.NewIterator(nil, nil)
}
