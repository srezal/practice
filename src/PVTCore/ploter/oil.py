from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Callable, List

import numpy as np
import plotly.graph_objects as go
import units
from plotly.subplots import make_subplots

if TYPE_CHECKING:
    from aggregator import ModelCorrelationAggregator
    from correlation.abstract import CorrelationVariable


class OilParamPloter:
    def __init__(
        self,
        max_press: units.Pressure = units.Pressure(500, units.PresUnit.Bar),
        max_sol: units.Solubility = units.Solubility(50, units.SolubilityUnit.m3_per_m3),
        min_temp: units.Temperature = units.Temperature(20, units.TempUnit.Celsius),
        max_temp: units.Temperature = units.Temperature(200, units.TempUnit.Celsius),
        pres_unit: units.PresUnit = units.PresUnit.Bar,
        fvf_unit: units.VolumeFactorUnit = units.VolumeFactorUnit.si,
        vis_unit: units.ViscUnit = units.ViscUnit.cP,
        sol_unit: units.SolubilityUnit = units.SolubilityUnit.m3_per_m3,
    ):
        self.min_press = units.Pressure(1, units.PresUnit.Bar)
        self.max_press = max_press
        self.num_press = 50
        self.min_sol = units.Solubility(10)
        self.max_sol = max_sol
        self.num_sol = 25
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.num_temp = 25
        self.pres_unit = pres_unit
        self.fvf_unit = fvf_unit
        self.vis_unit = vis_unit
        self.sol_unit = sol_unit

    def plot_param(
        self,
        var: CorrelationVariable,
        aggregator: ModelCorrelationAggregator,
    ) -> None:

        frames = []
        var = deepcopy(var)
        var.pres = units.Pressure.create(self.min_press, self.max_press, num=self.num_press)
        plot_temp = units.Temperature.generate(self.min_temp, self.max_temp, num=self.num_temp)

        for t_id, temp in enumerate(plot_temp):
            frame = self._get_frame(var, temp, aggregator)
            frames.append(frame)

        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=["Субплот 1", "Субплот 2", "Субплот 3", "Субплот 4"],
        )

        for pic in range(2):
            for line in range(self.num_temp):
                i = pic * self.num_temp + line
                fig.add_trace(frames[0].data[i], row=1, col=1 + pic)

        sliders = [
            {
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "",
                    "visible": True,
                    "xanchor": "right",
                },
                "transition": {"duration": 500, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [
                            [v.name],
                            {"frame": {"duration": 500, "redraw": True}, "mode": "immediate"},
                        ],
                        "label": v.name,
                        "method": "animate",
                    }
                    for k, v in enumerate(frames)
                ],
            }
        ]

        fig.update_layout(
            sliders=sliders,
            title="Анимация с субплотами и слайдером",
        )
        fig.frames = frames
        fig.show()

    def _get_frame(
        self,
        var: CorrelationVariable,
        temp: units.Temperature,
        aggregator,
    ) -> go.Frame:
        frame = go.Frame(
            name=f"Температура: {round(temp.kelvin()[0], 1)}",
            data=[
                *self._get_scatter(var, temp, aggregator.oil.fvf.calc, aggregator, self.fvf_unit),
                *self._get_scatter(var, temp, aggregator.oil.vis.calc, aggregator, self.vis_unit),
                # *self._get_scatter(var, temp, aggregator.oil.sol.calc, aggregator, self.sol_unit),
            ],
        )
        return frame

    def _get_scatter(
        self,
        var: CorrelationVariable,
        temp: units.Temperature,
        func: Callable[[CorrelationVariable], units.AbstractParam],
        aggregator,
        unit: units.AbstractUnit,
    ) -> List[go.Scatter]:
        results = []
        var = deepcopy(var)
        var.set_gas_oil_ratio(units.Solubility(np.array([np.inf])))
        var.temp = temp

        saturated = go.Scatter(
            x=var.pres.bar(),
            y=func(var).get(unit),
            mode="lines+markers",
            name="Линия насыщения",
            legendgroup="Линия насыщения",
            showlegend=True,
        )
        results.append(saturated)

        for sol in units.Solubility.generate(self.min_sol, self.max_sol, num=self.num_sol):
            var.set_gas_oil_ratio(sol)
            bbp = aggregator.oil.unsat.bpp.calc(var)
            var.pres = var.pres.cut(bbp, "more", "in")
            unsaturated = go.Scatter(
                x=var.pres.bar(),
                y=func(var).get(unit),
                mode="lines+markers",
                name=f"{sol.__class__.__name__}: {sol.value[0]}",
                legendgroup=f"{sol.__class__.__name__}: {sol.value[0]}",
                showlegend=True,
            )
            results.append(unsaturated)

        return results
