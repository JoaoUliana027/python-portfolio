from flask import Flask, render_template, request

app = Flask(__name__)

# Função para conversões
def convert_units(value, from_unit, to_unit):
    conversions = {
        "meter": {"kilometer": value / 1000, "centimeter": value * 100, "meter": value},
        "kilometer": {"meter": value * 1000, "centimeter": value * 100000, "kilometer": value},
        "centimeter": {"meter": value / 100, "kilometer": value / 100000, "centimeter": value},
        
        "gram": {"kilogram": value / 1000, "milligram": value * 1000, "gram": value},
        "kilogram": {"gram": value * 1000, "milligram": value * 1e6, "kilogram": value},
        "milligram": {"gram": value / 1000, "kilogram": value / 1e6, "milligram": value},
        
        "celsius": {
            "fahrenheit": (value * 9/5) + 32,
            "kelvin": value + 273.15,
            "celsius": value
        },
        "fahrenheit": {
            "celsius": (value - 32) * 5/9,
            "kelvin": ((value - 32) * 5/9) + 273.15,
            "fahrenheit": value
        },
        "kelvin": {
            "celsius": value - 273.15,
            "fahrenheit": ((value - 273.15) * 9/5) + 32,
            "kelvin": value
        }
    }

    return conversions.get(from_unit, {}).get(to_unit, None)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    units = [
        "meter", "kilometer", "centimeter",
        "gram", "kilogram", "milligram",
        "celsius", "fahrenheit", "kelvin"
    ]

    if request.method == "POST":
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]
            
            result = convert_units(value, from_unit, to_unit)

            if result is None:
                error = "Conversion not found."
        except ValueError:
            error = "Please enter a valid number."

    return render_template("index.html", result=result, error=error, units=units)

if __name__ == "__main__":
    app.run(debug=True)
