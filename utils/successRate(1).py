import json
import urllib2



def test_markov_successRate(testData):
	data_length = len(testData)
	successfulCount = 0
	for part in range(data_length - 1):
		current_id = testData[part]
		req = urllib2.Request('http://localhost:8000/home/seqRecommend?part=%s' % current_id)
		response = urllib2.urlopen(req)
		resStr  = response.read()
		flag = False
		res = json.loads(resStr)
		if res["isSuccessful"] == True:
			chain_count = len(res["recommend_list"])
			for each_chain in range(chain_count):
				part_count = len(res["recommend_list"][each_chain])
				for each_part in range(part_count):
					if res["recommend_list"][each_chain][each_part]["part_id"] == testData[part + 1]:
						flag = True
						successfulCount = successfulCount + 1
						break
				if flag == True:
					break
	successfulRate = float(successfulCount) / (data_length - 1)
	return [successfulRate,data_length - 1,successfulCount,data_length - successfulCount - 1]

def test_apriori_successRate(testData):
	data_length = len(testData)
	successfulCount = 0
	for part in range(data_length - 1):
		current_id = testData[part]
		req = urllib2.Request('http://localhost:8000/home/arecommend?seq=%d' % current_id)
		response = urllib2.urlopen(req)
		resStr  = response.read()
		res = json.loads(resStr)
		if res["isSuccessful"] == True:
			part_count = len(res["recommend_list"])
			for each_part in range(part_count):
				if res["recommend_list"][each_part]["part_id"] == testData[part + 1]:
					successfulCount = successfulCount + 1
					break
	successfulRate = float(successfulCount) / (data_length - 1)

	return [successfulRate,data_length - 1,successfulCount,data_length - successfulCount - 1]

testData1_1 = [188,151,163,145,144]
testData1_2 = [189,151,163,145,144]
testData1_3 = [190,151,163,145,144]
testData1_4 = [191,151,163,145,144]
testData1_5 = [187,151,156,145,144,189,151,158,145,144,191,151,154,145,144]
testData1_6 = [186,151,157,145,144,190,151,158,145,144,191,151,153,145,144]
testData2_1 = ["188","151","163","145","144"]
testData2_2 = ["189","151","163","145","144"]
testData2_3 = ["190","151","163","145","144"]
testData2_4 = ["191","151","163","145","144"]
testData2_5 = ["187","151","156","145","144","189","151","158","145","144","191","151","154","145","144"]
testData2_6 = ["186","151","157","145","144","190","151","158","145","144","191","151","153","145","144"]
print test_apriori_successRate(testData1_1)
print test_apriori_successRate(testData1_2)
print test_apriori_successRate(testData1_3)
print test_apriori_successRate(testData1_4)
print test_apriori_successRate(testData1_5)
print test_apriori_successRate(testData1_6)
print test_markov_successRate(testData2_1)
print test_markov_successRate(testData2_2)
print test_markov_successRate(testData2_3)
print test_markov_successRate(testData2_4)
print test_markov_successRate(testData2_5)
print test_markov_successRate(testData2_6)