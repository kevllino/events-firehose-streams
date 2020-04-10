from random import randint
import boto3
from pytictoc import TicToc

timer = TicToc()
car_manufacturers = ["Tesla", "Toyota", "Renault"]
ev_providers = ["Octopus", "EDF"]


def generate_random_signals(signal_size):
    car_signals = []
    user_signals = []

    for i in range(signal_size):
        car_signals.append(
            {"cableId": i, "carManufacturer": car_manufacturers[randint(0, len(car_manufacturers) - 1)]})
        user_signals.append({"userId": i, "evProvider": ev_providers[randint(0, len(ev_providers) - 1)]})

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
    client = boto3.client('firehose', region_name="eu-west-2")

    car_signals, user_signals = generate_random_signals(500)
    random_signals = car_signals + user_signals

    timer.tic()
    for signal in random_signals:
        if "cableId" in signal.keys():
            put_record(client, delivery_stream='cable-firehose-stream', record=signal)
        elif "userId" in signal.keys():
            put_record(client, delivery_stream='user-firehose-stream', record=signal)
    timer.toc("Put Record")

    timer.tic()
    put_record_batch(client, delivery_stream='cable-firehose-stream', records=car_signals)
    put_record_batch(client, delivery_stream='user-firehose-stream', records=user_signals)
    timer.toc("Put Records")
