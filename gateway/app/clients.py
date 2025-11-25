import httpx
from uuid import UUID
from .circuit_breaker import request_with_circuit_breaker

services = {
    "LOYALTY_URL": "http://loyalty:8050",
    "PAYMENT_URL": "http://payment:8060",
    "RESERVATION_URL": "http://reservation:8070",
}

client = httpx.Client(timeout=5.0)


def _fetch_hotels_raw(page: int, size: int) -> dict:
    r = client.get(
        f"{services['RESERVATION_URL']}/api/v1/hotels",
        params={"page": page, "size": size},
    )
    r.raise_for_status()
    return r.json()


def fetch_hotels(page: int, size: int) -> dict:
    return request_with_circuit_breaker("reservation", _fetch_hotels_raw, page, size)


def _fetch_user_reservations_raw(username: str) -> dict:
    r = client.get(
        f"{services['RESERVATION_URL']}/api/v1/me",
        headers={"X-User-Name": username},
    )
    r.raise_for_status()
    return r.json()


def fetch_user_reservations(username: str) -> dict:
    return request_with_circuit_breaker("reservation", _fetch_user_reservations_raw, username)


def _fetch_reservation_by_uid_raw(reservation_uid: UUID, username: str) -> dict:
    r = client.get(
        f"{services['RESERVATION_URL']}/api/v1/reservations/{reservation_uid}",
        headers={"X-User-Name": username},
    )
    r.raise_for_status()
    return r.json()


def fetch_reservation_by_uid(reservation_uid: UUID, username: str) -> dict:
    return request_with_circuit_breaker("reservation", _fetch_reservation_by_uid_raw, reservation_uid, username)


def _fetch_hotel_raw(hotel_uid: UUID) -> dict:
    r = client.get(
        f"{services['RESERVATION_URL']}/api/v1/hotel/{hotel_uid}"
    )
    r.raise_for_status()
    return r.json()


def fetch_hotel(hotel_uid: UUID) -> dict:
    return request_with_circuit_breaker("reservation", _fetch_hotel_raw, hotel_uid)


def _create_reservation_in_service_raw(res_data: dict, username: str) -> dict:
    r = client.post(
        f"{services['RESERVATION_URL']}/api/v1/reservations",
        headers={"X-User-Name": username},
        json=res_data,
    )
    r.raise_for_status()
    return r.json()


def create_reservation_in_service(res_data: dict, username: str) -> dict:
    return request_with_circuit_breaker("reservation", _create_reservation_in_service_raw, res_data, username)


def _create_payment_raw(price: int) -> dict:
    r = client.post(
        f"{services['PAYMENT_URL']}/api/v1/payments",
        json={"price": price},
    )
    r.raise_for_status()
    return r.json()


def create_payment(price: int) -> dict:
    return request_with_circuit_breaker("payment", _create_payment_raw, price)


def _fetch_payment_raw(payment_uid: UUID) -> dict:
    r = client.get(
        f"{services['PAYMENT_URL']}/api/v1/payments/{payment_uid}"
    )
    r.raise_for_status()
    return r.json()


def fetch_payment(payment_uid: UUID) -> dict:
    return request_with_circuit_breaker("payment", _fetch_payment_raw, payment_uid)


def _fetch_user_loyalty_raw(username: str) -> dict:
    r = client.get(
        f"{services['LOYALTY_URL']}/api/v1/me",
        headers={"X-User-Name": username},
    )
    r.raise_for_status()
    return r.json()


def fetch_user_loyalty(username: str) -> dict:
    return request_with_circuit_breaker("loyalty", _fetch_user_loyalty_raw, username)


def _update_loyalty_raw(username: str, delta: int) -> dict:
    r = client.patch(
        f"{services['LOYALTY_URL']}/api/v1/loyalty",
        headers={"X-User-Name": username},
        json={"delta": delta},
    )
    r.raise_for_status()
    return r.json()


def update_loyalty(username: str, delta: int) -> dict:
    return request_with_circuit_breaker("loyalty", _update_loyalty_raw, username, delta)


def _cancel_payment_raw(payment_uid: UUID) -> None:
    r = client.patch(
        f"{services['PAYMENT_URL']}/api/v1/payments/{payment_uid}/cancel",
    )
    r.raise_for_status()


def cancel_payment(payment_uid: UUID) -> None:
    return request_with_circuit_breaker("payment", _cancel_payment_raw, payment_uid)


def _cancel_reservation_raw(reservation_uid: UUID, username: str) -> None:
    r = client.patch(
        f"{services['RESERVATION_URL']}/api/v1/reservations/{reservation_uid}/cancel",
        headers={"X-User-Name": username},
    )
    r.raise_for_status()


def cancel_reservation(reservation_uid: UUID, username: str) -> None:
    return request_with_circuit_breaker("reservation", _cancel_reservation_raw, reservation_uid, username)
