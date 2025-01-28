from bokeh.palettes import HighContrast3
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource

def create_scatter_plot():
    # project data
    projects = ["Project A", "Project B", "Project C", "Project D", "Project E"]
    business_novelty = [10, 45, 27, 11, 50]
    customer_novelty = [13, 33, 22, 31, 55]
    impact = [15, 30, 25, 9, 17]  # Circle sizes


    data = {
        "projects": projects,
        "business_novelty": business_novelty,
        "customer_novelty": customer_novelty,
        "impact": impact
    }

    source = ColumnDataSource(data=data)


    p = figure(height=350, title="Project Portfolio Visualization", toolbar_location=None, tools="hover", tooltips="@projects: Business Novelty: @business_novelty, Customer Novelty: @customer_novelty, Impact: @impact")


    p.circle(x="business_novelty", y="customer_novelty", size="impact", color=HighContrast3[0], alpha=0.6, source=source)


    p.xaxis.axis_label = "Business Novelty"
    p.yaxis.axis_label = "Customer Novelty"
    p.y_range.start = 0
    p.x_range.start = 0
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    # Return script and div to embed in the HTML template
    script, div = components(p)
    return script, div