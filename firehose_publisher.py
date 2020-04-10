from random import randint
import boto3
from pytictoc import TicToc
import hcl

timer = TicToc()
car_manufacturers = ["Tesla", "Toyota", "Renault"]
ev_providers = ["Octopus", "EDF"]


def read_config(filename):
    with open(filename, 'r') as fp:
        object = hcl.load(fp)
    return object


def generate_random_signals(signal_size):
    car_signals = []
    user_signals = []

    for i in range(signal_size):
        car_signals.append({"cableId": i, "carManufacturer": car_manufacturers[randint(0, len(car_manufacturers) - 1)]})
        user_signals.append(
            {"userId": i, "name": "Enrique", "evProvider": ev_providers[randint(0, len(ev_providers) - 1)]})

    return car_signals, user_signals


def put_record(client, delivery_stream, record):
    response = client.put_record(
        DeliveryStreamName=delivery_stream,
        Record={"Data": f"{record}\n"}
    )
    return response


def put_record_batch(client, delivery_stream, records):
    response = client.put_record_batch(
        DeliveryStreamName=delivery_stream,
        Records=[
            {"Data": f"{record}\n"} for record in records
        ]
    )
    return response


if __name__ == '__main__':
    object = read_config("terraform/terraform.tfvars")
    car_stream_name, user_stream_name = object["car_stream_name"], object["user_stream_name"]

    client = boto3.client('firehose', region_name=object["region"])

    car_signals, user_signals = generate_random_signals(500)
    random_signals = car_signals + user_signals

    timer.tic()
    for signal in random_signals:
        if "cableId" in signal.keys():
            put_record(client, delivery_stream=car_stream_name, record=signal)
        elif "userId" in signal.keys():
            put_record(client, delivery_stream=user_stream_name, record=signal)
    timer.toc("Put Record")

    timer.tic()
    put_record_batch(client, delivery_stream=car_stream_name, records=car_signals)
    put_record_batch(client, delivery_stream=user_stream_name, records=user_signals)
    timer.toc("Put Records")
