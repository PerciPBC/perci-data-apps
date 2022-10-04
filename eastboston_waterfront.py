import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from numerize.numerize import numerize

SF_PER_ACRE = 43560

st.title('East Boston Waterfront for All')

st.write("""
East Boston, like much of the Greater Boston Area, is experiencing a housing crisis of unprecedented scale
driven by immense demand for housing, fueling development pressure and displacement. Once a 
naturally-affordable community for immigrant families to raise their children in the neighborhood's iconic
triple-deckers, as other parts of the city became more expensive, prices in East Boston have skyrocketed, buoyed
by the Blue Line's convenient access to downtown along with views of the city.
"""

# + """As a result, it's become increasingly hard for residents, especially more vulnerable renters, to be able to
# remain in a community they've been a part of for years. With smaller options primarily located within newer
# developments targeted for working professionals, older homeowners who no longer need as large of space
# aren't able to afford to downsize while still remaining in the neighborhood, locking in critically-needed inventory."""

+ """
To accomodate a growing population and build a better city, greater density is necessary and neighborhood change
is a prerequisite and will happen whether residents want it or not. Left to run its own course this drives
gentrification, but it doesn't have to be that way. We can build new homes while still retaining diversity and
supporting vulnerable communities.

One key place where a long-overdue conversation is finally emerging is the East Boston waterfront.

Read on to
learn more about what residents could make possible here!
""")

st.header("East Boston by the numbers")

households_homes = pd.DataFrame([
        ["<$35K (<30% AMI)", 4486, 1806 + 1216],
        ["$35K to $49,999 (<50% AMI)", 2035, 1542],
        ["$35,000 to $74,999 (<60% AMI)", 3230, 1968],
        ["$75,000+ (>80% AMI)", 7333, 661]
    ],
    columns=['Income', '# Households', '# Cost-burdened Households']
)
households_homes['% Cost-burdened'] = 100 * households_homes['# Cost-burdened Households'] / households_homes['# Households']

cost_burdened_households = int(households_homes['# Cost-burdened Households'].sum())
income_restricted_homes = 2761

a_col1, a_col2, a_col3, a_col4 = st.columns(4)
a_col1.metric("Households", numerize(17123))
a_col2.metric("Cost-burdened households", numerize(cost_burdened_households))
a_col3.metric("Income-restricted homes", numerize(income_restricted_homes))
a_col4.metric("Income-restricted home gap", numerize(cost_burdened_households - income_restricted_homes))

st.markdown("""
- Using the typical threshold, a cost-burdened household is one that spends >30% of its income on housing-related
  costs, such as rent and mortgage
- Income-restricted homes are a type of affordable housing that requires certain incomes to qualify. Because the
  need for affordable housing is greater than the supply, lotteries and long waiting lists are required. 
""")

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# Display a static table
st.table(households_homes)

st.caption("Sources: U.S. Census Bureau - American Community Survey 2020; City of Boston Open Data Portal")
st.header("The East Boston Designated Port Area")

st.write("""
With the East Boston Designated Port Area (boundaries marked in red in the map below),
there's a massive opportunity to help address the crisis. 

Because these properties are within a Designated Port Area, state regulations limit their
use to marine-industrial purposes. As a result, there are severe restrictions
on what can and cannot happen within the boundaries, unless the properties are removed
or the DPA regulations are modified.
""")

dpa_acres = 33

b_col1, b_col2, b_col3, b_col4 = st.columns(4)
b_col1.metric("Available Acres", dpa_acres)
b_col2.metric("Current homes", 0)
b_col3.metric("Currently allowed homes", 0)

components.iframe(
    "https://felt.com/embed/map/East-Boston-Designated-Port-Area-PvTqoiSzSGK2YxtGu2Z4OC?lat=42.371475&lon=-71.032965&zoom=14.284",
    height = 300)

st.subheader("How should the East Boston DPA be redeveloped?")

st.write("""
Now it's your turn! Use the sliders below to see what happens when you change redevelopment parameters.

This is part of what urban planners do when creating new zoning that will regulate land use and development.
""")

open_space = st.slider("How much should be set aside as open space (e.g. parks)?",
    min_value = 0,
    max_value = 100,
    format = '%d%%',
    value = 50
)

residential_floors = st.slider("How many floors should be built on top of a ground floor of commercial space?",
    min_value = 1,
    max_value = 30,
    value = 5
)

parking_ratio = st.slider("How many homes should there be per parking spot? (Higher means less parking)",
    min_value = 0,
    max_value = 100,
    value = 10
)

open_space_acres = dpa_acres * open_space / 100
developable_sf = (dpa_acres - open_space_acres) * SF_PER_ACRE
commercial_gsf = developable_sf
residential_gsf = developable_sf * residential_floors
total_gsf = commercial_gsf + residential_gsf
commercial_usable_gsf = commercial_gsf * .85
residential_usable_gsf = residential_gsf * .85
parking_allocation_per_home = 350 / parking_ratio if parking_ratio > 0 else 0
homes = residential_usable_gsf / (1000 + parking_allocation_per_home) 
parking_spots = homes / parking_ratio if parking_ratio > 0 else 0

st.write("With these primary constraints, the East Boston DPA would become...")

c_col1, c_col2, c_col3, c_col4 = st.columns(4)
c_col1.metric("New open space", open_space_acres)
c_col2.metric("Commercial floor area", numerize(commercial_gsf, 1))
c_col3.metric("Homes", numerize(homes))
c_col4.metric("Parking spots", numerize(parking_spots, 0))

st.subheader("""
How much value can redevelopment create?
""")

st.write("""
Of course, there's also the practical side of things. Redevelopment won't happen unless
there's new value being created (or taxpayers fund it). After all, you need to pay for
materials and labor to build things.

Land is valuable when it gets used. For example, a farmer can plant crops to grow and sell. The value is
influenced both by the market (supply and demand), the characteristics of the property, and regulations that constrain it.

The properties within the DPA are less valuable today because their use is limited to marine-industrial.
As you can see below, by lifting that restriction and allowing for mixed-use redevelopment, the value that
could be created is potentially quite high.

A lot has changed in recent years in the housing market, so these factors are a bit of a 
moving target. We'll talk a bit about how the risk and value get shared between players below.
""")

hard_cost_psf = st.slider("How much does it cost to build per sq. ft.?",
    min_value = 0,
    max_value = 800,
    value = 350,
    format = '$%d'
)

soft_cost_ratio = st.slider("How much are \"soft\" costs as a percentage of construction costs? (e.g. architecture, engineering, legal fees)",
    min_value = 0,
    max_value = 100,
    value = 30,
    format = '%d%%',
)

residential_price_psf = st.slider("What's the market-rate price of new homes per sq. ft.?",
    min_value = 0,
    max_value = 1500,
    value = 900,
    format = '$%d'
)

commercial_price_psf = st.slider("What's the market-rate price of commercial space per sq. ft.?",
    min_value = 0,
    max_value = 1000,
    value = 250,
    format = '$%d'
)

hard_cost = total_gsf * hard_cost_psf
development_cost = hard_cost * (1 + soft_cost_ratio / 100)
commercial_revenue = commercial_price_psf * commercial_usable_gsf
residential_revenue = residential_price_psf * residential_usable_gsf
potential_revenue = commercial_revenue + residential_revenue
project_value = potential_revenue - development_cost

c_col1, c_col2, c_col3, c_col4 = st.columns(4)
c_col1.metric("Development cost", '$' + numerize(development_cost))
c_col2.metric("Potential revenue", '$' + numerize(potential_revenue))
c_col3.metric("Total value", '$' + numerize(project_value))

st.subheader("""
How should this pie get split?
""")

st.markdown("""
This value and the uncertainty of how much the value will actually be (risk) gets shared between participants
in the project:
- Existing Landowner - Sells ownership in the project (low risk), retains ownership (high risk), or sells a portion. 
    The amount of equity sold is dependent on the owner's risk tolerance
- Developer - Manages the overall project, typically for a flat fee and/or equity in the project (to share in the profits)
- Investors - Finances the project and takes on the risk
    - Banks - Provides cash in exchange for a fixed higher future repayment through interest (lower risk)
    - Limited Partners (LPs) - Provides cash (and/or expertise/services) for variable repayment based on actual profits (highest risk)   
- Public - Captures a portion of project value through public benefits (e.g. income-restricted affordable housing)
    and property taxes to fund infrastructure and public services (e.g. schools)

Some things are private matters, dictated by individual circumstances and business needs, like how to compensate
a developer for managing a project. Others, like how much income-restricted affordable housing gets created, is 
a function of both the market and of policy. 

Finally, there's also the potential for value creation through externalities outside of the bounds of the project.
For example, if the project creates new parkspace, it could make nearby properties more appealing, including their 
market value. Some call this the "halo effect" and it needs to be appropriately managed to avoid downsides,
such as green gentrification. In the choices below, measures are in place to promote a project being in the overall
benefit of vulnerable communities.

Lawmakers create policy and you elect lawmakers, so you have the power to influence what happens!
""")

affordable_housing_pct = st.slider("What percentage of homes should be income-restricted (\"affordable\") housing?",
    min_value = 0,
    max_value = 100,
    value = 20,
    format = '%d%%',
)

development_fee_pct = st.slider("What percentage of the construction costs should the developer get for creating new housing?",
    min_value = 0,
    max_value = 100,
    value = 10,
    format = '%d%%',
)

land_cost_per_gsf = st.slider("How much should the existing landowner get for selling their land per developed sq. ft.?",
    min_value = 0,
    max_value = 500,
    value = 35,
    format = '$%d'
)

addl_public_benefits_pct = st.slider("What percentage of the construction costs should be paid towards additional public benefits, like building parks or climate resiliency?",
    min_value = 0,
    max_value = 20,
    value = 5,
    format = '%d%%',
)

income_restricted_housing = affordable_housing_pct / 100 * homes 
blended_psf = residential_price_psf - (residential_price_psf - 200) * affordable_housing_pct / 100
adjusted_revenue = blended_psf * residential_usable_gsf + commercial_revenue
development_fee = hard_cost * development_fee_pct / 100
landowner_payout = total_gsf * land_cost_per_gsf
addl_public_benefits = hard_cost * addl_public_benefits_pct / 100

d_col1, d_col2, d_col3, d_col4 = st.columns(4)
d_col1.metric("Income-restricted homes", round(income_restricted_housing))
d_col2.metric("Development fee", '$' + numerize(development_fee, 1))
d_col3.metric("Landowner payout", '$' + numerize(landowner_payout, 1))
d_col4.metric("Addl. public benefits", '$' + numerize(addl_public_benefits, 1))

profit = adjusted_revenue - development_cost - development_fee - landowner_payout - addl_public_benefits
profit_margin = profit / adjusted_revenue

st.write("""
What remains is profit for the investors (equityholders). Given the scale of potential projects here, the
numbers might be quite big, but you'll have to normalize it to have a sense of how it compares with other
ways investors could choose to use their money (e.g. buy stocks and bonds).

Remember, there's a competitive market for investment opportunities, so this needs to be appealing enough
for the people who can finance it for them to risk potential losses for a project to happen.
""")

e_col1, e_col2, e_col3, e_col4 = st.columns(4)
e_col1.metric("Profit", '$' + numerize(profit, 1))
e_col2.metric("Profit Margin", numerize(profit_margin * 100, 1) + '%')

st.write("""
Hopefully, you learned a thing or two here. Now comes the hard part of reconciling different perspectives
to land on a compromise that appeases as many people as possible while still meeting the overall goal
of ultimately creating a better East Boston Waterfront for All.

Have ideas or feedback? Let us know at hello[at]perci.app. 
""")