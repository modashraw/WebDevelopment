import React, { useState } from "react";
import Card from "../UI/Card";
import ExpenseFilter from "./ExpensesFilter";
import ExpensesList from "./ExpensesList";
import "./Expenses.css";
import ExpensesChart from "./ExpensesChart";

const Expenses = (props) => {
    /** Set current year to filter */
    const currentYear = new Date().getFullYear().toString();

    /** Filter state and handleFunction */
    const [filteredYear, setFilteredYear] = useState(currentYear);
    const filterChangeHandler = (selectedYear) => {
        setFilteredYear(selectedYear);
    };

    /** Filter list based on selected year */
    const filteredExpenses = props.items.filter((item) => {
        return (
            !filteredYear || item.date.getFullYear().toString() === filteredYear
        );
    });

    return (
        <Card className="expenses">
            <ExpenseFilter
                selectedValue={filteredYear}
                onFilterChange={filterChangeHandler}
            />
            <ExpensesChart expenses={filteredExpenses}></ExpensesChart>
            <ExpensesList items={filteredExpenses} />
        </Card>
    );
};

export default Expenses;
