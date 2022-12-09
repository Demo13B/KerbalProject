import krpc
conn = krpc.connect(name='Status Check')
print(conn.krpc.get_status().version)
print('Connection established\nReady for Launch')

