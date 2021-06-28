//App is a special component. Kind of root component
import React, { useState } from "react";
import NewExpense from "./components/NewExpense/NewExpense";
import Expenses from "./components/Expenses/Expenses";
import "./App.css";

const App = () => {
    const initialExpenses = [
        {
            id: 1,
            title: "Toilet Paper",
            amount: 94.12,
            date: new Date(2020, 7, 14),
        },
        {
            id: 2,
            title: "New TV",
            amount: 799.49,
            date: new Date(2021, 2, 12),
        },
        {
            id: 3,
            title: "Car Insurance",
            amount: 294.67,
            date: new Date(2021, 2, 28),
        },
        {
            id: 4,
            title: "New Desk (Wooden)",
            amount: 450,
            date: new Date(2021, 5, 12),
        },
    ];

    const [expenses, setNewExpense] = useState(initialExpenses);

    const addExpenseHandler = (expense) => {
        setNewExpense((prevExpenses) => {
            return [expense, ...prevExpenses];
        });
    };

    return (
        <div className="App">
            <h2>Expense Tracker</h2>
            <NewExpense onAddExpense={addExpenseHandler} />
            <Expenses items={expenses} />
        </div>
    );
};
export default App;
