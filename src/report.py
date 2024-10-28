from jinja2 import Template


html_template = """
<html>
<head><title>Report</title></head>
<body>
    <h1>MySQL comparator</h1>

    <h2>Overall Comparisson</h2>


    <h3>1 Versions</h3>
    <table id="table_versions" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_versions %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>2 Variables</h3>
    <table id="table_variables" border="1">
        <tr>
            <th>Key</th>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_variables %}
        <tr>
            <td>{{ row.key }}</td>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>3 Schemas List</h3>
    <table id="table_schemas" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_schemas %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>4 Tables</h3>
    <table id="table_tables" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_tables %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>5 Views</h3>
    <table id="table_views" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_views %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>6 Constraints</h3>
    <table id="table_constraints" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_constraints %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>7 Indexes</h3>
    <table id="table_indexes" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_indexes %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>8 Partitions</h3>
    <table id="table_partitions" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_partitions %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>9 Stored Procedures</h3>
    <table id="table_stored_procedures" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_stored_procedures %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>10 Triggers</h3>
    <table id="table_triggers" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_triggers %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>11 User and Hosts</h3>
    <table id="table_user_and_hosts" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_user_and_hosts %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>

    <h3>12 User and Permissions</h3>
    <table id="table_user_and_permissions" border="1">
        <tr>
            <th>Blue</th>
            <th>Green</th>
            <th>Result</th>
        </tr>
        {% for row in table_user_and_permissions %}
        <tr>
            <td>{{ row.blue }}</td>
            <td>{{ row.green }}</td>
            <td>{{ row.result }}</td>
        </tr>
        {% endfor %}
    </table>


    <h2>Count tables</h2>
    <p>more here</p>
</body>
</html>
"""

def generate_general_report(data):

    # Create the template
    template = Template(html_template)

    # Render the template with data
    rendered_html = template.render(
        table_versions = data["QUERY_01_VERSIONS"],
        table_variables = data["QUERY_02_VARIABLES"],
        table_schemas = data["QUERY_03_SCHEMAS_LIST"],
        table_tables = data["QUERY_04_LIST_TABLES"],
        table_views = data["QUERY_05_LIST_VIEWS"],
        table_constraints = data["QUERY_06_LIST_CONSTRAINTS"],
        table_indexes = data["QUERY_07_LIST_INDEXES"],
        table_partitions = data["QUERY_08_LIST_PARTITIONS"],
        table_stored_procedures = data["QUERY_09_LIST_STORED_PROCEDURES"],
        table_triggers = data["QUERY_10_LIST_TRIGGERS"],
        table_user_and_hosts = data["QUERY_11_LIST_USERS_AND_HOSTS"],
        table_user_and_permissions = data["QUERY_12_LIST_USERS_AND_ITS_PERMISSIONS"]
    )

    # Save the report to an HTML file
    with open('report_mysql.html', 'w') as file:
        file.write(rendered_html)

    print("Report generated successfully.")