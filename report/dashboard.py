from fasthtml.common import *  # noqa: F403
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parents[1]))

# Import QueryBase, Employee, Team from employee_events
from employee_events.query_base import QueryBase  # noqa: E402
from employee_events.employee import Employee  # noqa: E402
from employee_events.team import Team  # noqa: E402

# import the load_model function from the utils.py file
from report.utils import load_model  # noqa: E402

# Import base and combined components
from base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable  # noqa: E402
from combined_components import FormGroup, CombinedComponent  # noqa: E402

# ---------------------------
# Custom Components
# ---------------------------

class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        return model.names()


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        title = "Employee Performance" if model.name == "employee" else "Team Performance"
        return H1(title)  # noqa: F405


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        if not entity_id:
            return

        df = model.event_counts(entity_id)
        df = df.fillna(0)
        df = df.set_index("event_date")
        df = df.sort_index()
        df = df.cumsum()
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        df.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        ax.set_title("Cumulative Event Counts", fontsize=11, pad=15)
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        return fig


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        if not entity_id:
            return

        data = model.model_data(entity_id)
        probabilities = self.predictor.predict_proba(data)[:, 1]

        if model.name == "team":
            pred = probabilities.mean()
        else:
            pred = probabilities[0]

        if pred < 0.33:
            color = "green"
        elif pred < 0.66:
            color = "yellow"
        else:
            color = "red"

        fig, ax = plt.subplots()
        ax.barh([''], [pred], color=color)
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        return fig


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')  # noqa: F405


class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]


class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), NotesTable()]

    def __call__(self, entity_id, model):
        self.userId = entity_id
        self.model = model

        dynamic_children = [
            Header(),
            DashboardFilters(),
            NotesTable(),
        ]

        if self.userId and self.model:
            dynamic_children.insert(2, Visualizations())  # Add Visualizations before NotesTable

        self.children = dynamic_children
        return super().__call__(entity_id, model)


# ---------------------------
# Initialize app and report
# ---------------------------
app = FastHTML()  # noqa: F405
report = Report()


# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def index():
    return report(None, QueryBase())


@app.get("/employee/{employee_id}")
def employee(employee_id: str):
    return report(employee_id, Employee())


@app.get("/team/{team_id}")
def team(team_id: str):
    return report(team_id, Team())


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params['profile_type']
    if profile_type == 'Team':
        return dropdown(None, Team())
    elif profile_type == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()  # noqa: F405
