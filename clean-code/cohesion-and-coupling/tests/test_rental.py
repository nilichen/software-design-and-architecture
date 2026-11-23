from datetime import date

import events
import payments
from rental import Customer, Extra, RentalContract, Vehicle

ANA = Customer("Ana Silva", "ana.silva@example.com")
SUV = Vehicle("suv", rate=4_500, free_km=100)


def contract(**kwargs) -> RentalContract:
    return RentalContract(
        "B1", ANA, SUV, days=3, km=450, pickup=date(2026, 12, 1), **kwargs
    )


def test_any_vehicle_can_be_priced_without_a_catalogue():
    test_car = Vehicle("test", rate=1_000, free_km=0)
    assert test_car.price(days=2, km=4) == 2_100


def test_removing_an_extra_removes_its_price():
    c = contract()
    c.add_extra(Extra("gps", 1_000))
    c.add_extra(Extra("child_seat", 500))
    c.remove_extra("gps")
    assert c.extras == [Extra("child_seat", 500)]
    assert c.total_price() == 17_250 + 500


def test_discount_does_not_change_the_contract():
    c = contract(discount_percent=10)
    assert c.discounted_price() == 15_525
    assert c.discounted_price() == 15_525
    assert c.total_price() == 17_250


def test_credit_adds_the_card_fee():
    assert payments.pay_credit("4000000000001111", 17_250).amount == 17_595


def test_publish_reaches_every_subscriber():
    received = []
    events.subscribe("test_event", received.append)
    events.subscribe("test_event", lambda data: received.append(data["id"]))
    events.publish("test_event", {"id": "B1"})
    assert received == [{"id": "B1"}, "B1"]
