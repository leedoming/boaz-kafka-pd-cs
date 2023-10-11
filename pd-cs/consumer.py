import csv
import json
import os
import time

from kafka import KafkaConsumer


class Consumer:
    def __init__(self, brokers, topicName):
        self.consumer = KafkaConsumer(
            topicName,
            group_id="consumer-group-v3",
            bootstrap_servers=brokers,
            api_version=(0, 11, 5),
        )

    def income_check(self):
        print("Start state check")
        new_data = []  # 새로운 데이터 저장
        for message in self.consumer:
            data = json.loads(message.value.decode())
            # print(data)
            # 종료 신호인 경우
            if data["row"][0] == "DONE":
                break
            # income이 $120K 이상인 경우
            if "Texas" in str(data["row"][4]):
                print("--State Texas")
                # account, name, street, city, state, Jan, Feb, Mar 정보만 저장
                new_row = [data["row"][0], data["row"][1], data["row"][2], data["row"][3], data["row"][4], data["row"][6], data["row"][7], data["row"][8]]
                new_data.append(new_row)

                print(f'{data["index"]} {new_row.__str__()}')

                # csv 파일 업데이트
                file_name = "./state_Texas.csv"
                file_path = os.path.join(os.path.dirname(__file__), file_name)
                with open(file_path, "a", newline='') as f:
                    writer = csv.writer(f)
                    if os.stat(file_path).st_size == 0:  # 파일이 비어있으면 헤더 추가
                        writer.writerow(['account', 'name', 'street', 'city', 'state', 'Jan', 'Feb', 'Mar'])
                    writer.writerow(new_row)


        print("End State check")


if __name__ == '__main__':
    brokers = ["localhost:9092"]
    topicName = "boaz"
    consumer = Consumer(brokers, topicName)
    consumer.income_check()
