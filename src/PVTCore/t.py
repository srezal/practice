import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Создаем фигуру с 2 строками и 1 колонкой
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=["Субплот 1", "Субплот 2"]
)

# Данные по оси X
x = [1, 2, 3, 4, 5]

# Начальные данные для первого кадра
y1_start = [1, 2, 3, 4, 5]
y2_start = [5, 4, 3, 2, 1]



# Создаем кадры (frames) для анимации
frames = []
for k in range(1, 6):
    y1 = [v * k for v in y1_start]
    y2 = [v * (6 - k) for v in y2_start]

    frames.append(
        go.Frame(
            name=f"Кадр {k}",
            data=[
                go.Scatter(x=x, y=y1, mode="lines+markers", name="Линия 1", legendgroup="Линия 1", showlegend=False),  # 1-й subplot
                go.Scatter(x=x, y=y1, mode="lines+markers", name="Линия 2", legendgroup="Линия 2", showlegend=True),  # 2-й subplot
                go.Scatter(x=x, y=y2, mode="lines+markers", name="Линия 1", legendgroup="Линия 2", showlegend=True),  # 1-й subplot
                go.Scatter(x=x, y=y2, mode="lines+markers", name="Линия 2", legendgroup="Линия 1", showlegend=False),  # 2-й subplot

            ]
        )
    )

# Добавляем стартовые трэйсы (они будут заменяться при анимации)
fig.add_trace(frames[0].data[0], row=1, col=1)
fig.add_trace(frames[0].data[1], row=2, col=1)
fig.add_trace(frames[0].data[2], row=1, col=1)
fig.add_trace(frames[0].data[3], row=2, col=1)

# Добавляем слайдер для ручного выбора кадра
sliders = [
    {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Кадр: ",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 500, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [
            {
                "args": [[f"Кадр {k}"],
                         {"frame": {"duration": 500, "redraw": True}, "mode": "immediate"}],
                "label": f"{k}",
                "method": "animate"
            } for k in range(1, 6)
        ]
    }
]


# Применяем обновления к макету
fig.update_layout(
    sliders=sliders,
    title="Анимация с субплотами и слайдером"
)

# Добавляем кадры
fig.frames = frames

fig.show()
