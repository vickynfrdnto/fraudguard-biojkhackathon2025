from pydantic import BaseModel


class SummaryCard(BaseModel):
    title: str
    value: str
    icon: str
    bg: str
    text: str
    change: str
    changeColor: str


class DashboardSummary(BaseModel):
    cards: list[SummaryCard]


class ChartDataset(BaseModel):
    label: str
    data: list[int | float]
    borderColor: str | None = None
    backgroundColor: str | list[str] | None = None
    tension: float | None = None
    fill: bool | None = None


class ChartResponse(BaseModel):
    labels: list[str]
    datasets: list[ChartDataset]


class AlertOut(BaseModel):
    type: str
    desc: str
    time: str
    color: str


class AnalyticsSummary(BaseModel):
    label: str
    value: str
    color: str
