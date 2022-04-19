login_info = [
    [['202034533', 'wuweimeng123'], ['202036955', 'wzh168169']],  # 周一 约周四 1+1/3个号 晚上*2
    [['202036955', 'wzh168169'], ['201916207', 'my412427']],  # 周二 约周五 1+1/3个号 晚上*2
    [['201916202', 'dzthang96102'], ['202016949', '.980206zxh.']],  # 周三 约周六 两个号 下午*2晚上*2
    [['201936225', 'Zz837868!'], ['201820627', 'mjx900619']],  # 周四 约周日 两个号 下午*2晚上*2
    [['202136976', 'lxj990212lxj']],  # 周五 约周一 2/3个号
    [['202016944', 'gsk199938'], ['201916207', 'my412427']],  # 周六 约周二 1+1/3个号
    [['202016948', 'ladida52459'], ['202036957', 'yb199692']]  # 周天 约周三 两个号
]
order_list = [
    [['16:00-17:30', '16:00-17:30', '16:00-17:30'], ['20:00-21:30']],  # 周一约周四
    [['18:30-20:00', '20:00-21:30'], ['18:30-20:00', '20:00-21:30']],  # 周二约周五
    [['16:00-17:30', '18:30-20:00', '20:00-21:30'], ['16:00-17:30', '18:30-20:00', '20:00-21:30']],  # 周三约周六
    [['16:00-17:30', '18:30-20:00', '20:00-21:30'], ['16:00-17:30', '18:30-20:00', '20:00-21:30']],  # 周四约周日
    [['16:00-17:30', '16:00-17:30']],  # 周五约周一
    [['18:30-20:00', '20:00-21:30', '18:30-20:00'], ['20:00-21:30']],  # 周六约周二
    [['16:00-17:30', '18:30-20:00', '20:00-21:30'], ['16:00-17:30', '18:30-20:00', '20:00-21:30']]  # 周日约周三
]

preference = [9, 8, 7, 6, 10, 3, 2, 1, 4, 5, 12, 11]

json = {
	"header": {
		"code": 0,
		"message": {
			"title": "",
			"detail": ""
		}
	},
	"body": {
		"dataStores": {
			"uploader_grid_grid_0": {
				"rowSet": {
					"primary": [],
					"filter": [],
					"delete": []
				},
				"name": "uploader_grid_grid_0",
				"pageNumber": 1,
				"pageSize": 2147483647,
				"recordCount": 0,
				"rowSetName": "uploader_grid_grid_0",
				"parameters": {
					"grid_name": "使用人员"
				}
			},
			"variable": {
				"rowSet": {
					"primary": [{
						"name": "JHYYSJ",
						"source": "process",
						"type": "string",
						"value": "2022-04-21",
						"_t": 1,
						"_o": {
							"value": ""
						}
					}, {
						"name": "XH",
						"source": "process",
						"type": "string",
						"value": "202036957",
						"_t": 1,
						"_o": {
							"value": ""
						}
					}, {
						"name": "XM",
						"source": "process",
						"type": "string",
						"value": "杨彬",
						"_t": 1,
						"_o": {
							"value": ""
						}
					}, {
						"name": "CD",
						"source": "process",
						"type": "string",
						"value": "10号场地",
						"_t": 1,
						"_o": {
							"value": ""
						}
					}, {
						"name": "XZSD",
						"source": "process",
						"type": "string",
						"value": "8:00-9:30",
						"_t": 1,
						"_o": {
							"value": ""
						}
					}, {
						"name": "BUSINESS_UNIT",
						"source": "process",
						"type": "string",
						"value": ""
					}, {
						"name": "SYRS",
						"source": "process",
						"type": "string",
						"value": "4",
						"_t": 1,
						"_o": {
							"value": ""
						}
					}, {
						"name": "SYS_USER",
						"source": "interface",
						"type": "string",
						"value": "杨彬"
					}, {
						"name": "SYS_UNIT",
						"source": "interface",
						"type": "string",
						"value": "海洋研究院 "
					}, {
						"name": "SYS_DATE",
						"source": "interface",
						"type": "date",
						"value": "1650369040638"
					}],
					"filter": [],
					"delete": []
				},
				"name": "variable",
				"pageNumber": 1,
				"pageSize": 2147483647,
				"recordCount": 0,
				"parameters": {}
			},
			"8ccd29da-6b69-46d4-b72f-55bde180": {
				"rowSet": {
					"primary": [],
					"filter": [],
					"delete": []
				},
				"name": "8ccd29da-6b69-46d4-b72f-55bde180",
				"pageNumber": 1,
				"pageSize": 2147483647,
				"recordCount": 0,
				"parameters": {
					"exist": "true",
					"relatedcontrols": "grid_0",
					"primarykey": "pk_id",
					"queryds": "8ccd29da-6b69-46d4-b72f-55bde180",
					"gridds": "true"
				}
			},
			"dbe32bfd-920a-4bb0-b077-c5444402": {
				"rowSet": {
					"primary": [{
						"SYRS": "4",
						"FYCCBH": "2022-04-21青岛校区10号场地",
						"pk_id": "3863061e:1803b813211:37d8",
						"SZXQ": "青岛校区",
						"QTLX": "",
						"YCHYQYY": "",
						"XZSYSD_TEXT": "8:00-9:30",
						"KNLX": "",
						"JHYYSJ": "2022-04-21",
						"XZXQ": "2022-04-21青岛校区",
						"JHYYSJ_TEXT": "2022-04-21",
						"YCGDZ": "",
						"fk_id": "2204191937169132",
						"text": "",
						"XZXQ_TEXT": "青岛校区",
						"SYCD": "10号场地",
						"SQCS": "2",
						"ZXSGH": "",
						"KNLXGDZ": "",
						"XH": "202036957",
						"FYCCBH_TEXT": "10号场地",
						"ZJ": "",
						"XYKNGDZ": "",
						"PD": "0",
						"XM": "杨彬",
						"SYNF": "2022",
						"SYZQ": "2022-04-21",
						"XZSYSD": "2022-04-21青岛校区10号场地8:00-9:30",
						"_t": 3,
						"_o": {
							"JHYYSJ_TEXT": "请选择",
							"JHYYSJ": "",
							"XZXQ_TEXT": "",
							"XZXQ": "",
							"FYCCBH_TEXT": "请选择",
							"FYCCBH": "",
							"XZSYSD_TEXT": "请选择",
							"XZSYSD": "",
							"SYZQ": "",
							"SYNF": "",
							"SYCD": "请选择",
							"SQCS": "0"
						}
					}],
					"filter": [],
					"delete": []
				},
				"name": "dbe32bfd-920a-4bb0-b077-c5444402",
				"pageNumber": 1,
				"pageSize": 2147483647,
				"recordCount": 0,
				"rowSetName": "876aa03d-070b-4551-8c52-a5c24361",
				"parameters": {
					"exist": "true",
					"relatedcontrols": "body_0",
					"primarykey": "pk_id",
					"queryds": "dbe32bfd-920a-4bb0-b077-c5444402"
				}
			}
		},
		"parameters": {
			"formid": "408225d8-1abe-4cdd-8a0d-fd8b1c6f",
			"SYS_FK": "2204191937169132",
			"privilegeId": "711549755616fbc517757f5036364348",
			"seqId": "",
			"status": "select",
			"service_id": "755b2443-dda6-47b6-ba0c-13f5f1e39574",
			"process": "2ff0b7de-9c31-4898-94ac-adfd3e3eebca",
			"seqPid": "",
			"strUserId": "",
			"strUserIdCC": "",
			"nextActId": ""
		}
	}
}