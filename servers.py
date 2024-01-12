#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import re


class Product:
    def __init__(self, name: str, price: float) -> None:
        if re.match('^[a-zA-Z]+\\d+$', name) is None:
            raise ValueError
        else:
            self.name = name
            self.price = price

    def __eq__(self, other) -> bool:
        return (self.name == other.name) and (self.price == other.price)

    def __hash__(self) -> int:
        return hash((self.name, self.price))


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


class Server(ABC):
    n_max_returned_entries: int = 3
    def __init__(self, *args, **kwargs) ->None:
        super.__init__(*args, **kwargs)

    def get_entries(self, n_letters) ->List[Product]:
        pattern = '^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters)
        entries = [prod for prod in self.get_all_products(n_letters) if re.match(pattern, prod.name)]
        if len(entries) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(entries, key=lambda prod: prod.price)

    @abstractmethod
    def get_all_products(self, n_letters: int = 3) -> List[Product]:
        raise NotImplementedError


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products_: List[Product] = products

    def get_all_products(self, n_letters: int = 3) -> List[Product]:
        return self.products_


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products_: Dict[str, Product] = {product.name: product for product in products}

    def get_all_products(self, n_letters: int = 3) -> List[Product]:
        return list(self.products_.values())


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()