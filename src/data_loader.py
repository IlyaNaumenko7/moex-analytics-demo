"""Модуль для загрузки исторических данных с биржи."""

import pandas as pd
import yfinance as yf


class MOEXDataLoader:
    """
    Загрузчик исторических OHLCV-данных.

    По умолчанию использует Yahoo Finance (формат тикера 'SBER.ME' для MOEX).
    Легко заменяется на любой другой источник — интерфейс класса сохраняется.
    """

    def __init__(self, ticker: str):
        """
        Args:
            ticker: Тикер инструмента.
                    Для акций MOEX используется формат 'TICKER.ME' (например, 'SBER.ME').
                    Для US акций — просто 'AAPL', 'MSFT' и т.д.
        """
        # Если пользователь передал просто 'SBER', добавляем '.ME'
        if "." not in ticker:
            self.ticker = f"{ticker.upper()}.ME"
        else:
            self.ticker = ticker.upper()

    def get_history(
        self,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Загружает исторические OHLCV-данные.

        Args:
            start_date: Начальная дата в формате 'YYYY-MM-DD'.
            end_date: Конечная дата в формате 'YYYY-MM-DD'.
            interval: Интервал свечей ('1d', '1wk', '1mo').

        Returns:
            DataFrame с колонками: date, open, high, low, close, volume.

        Raises:
            ValueError: Если данные пусты или произошла ошибка.
        """
        try:
            stock = yf.Ticker(self.ticker)
            df = stock.history(start=start_date, end=end_date, interval=interval)

            if df.empty:
                raise ValueError(f"Нет данных для тикера {self.ticker}")

            # Приводим к единому формату
            df = df.reset_index()
            df = df.rename(columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            })

            # Убираем часовой пояс для единообразия
            df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

            df = df[["date", "open", "high", "low", "close", "volume"]]
            df = df.sort_values("date").reset_index(drop=True)

            return df

        except Exception as e:
            raise ValueError(f"Ошибка загрузки данных для {self.ticker}: {e}")