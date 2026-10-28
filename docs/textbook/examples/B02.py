for input_value in (0, 5, 100):
    output_value = input_value * 2
    print(f"input={input_value}; state A={input_value}; output={output_value}")
    assert output_value == input_value + input_value
