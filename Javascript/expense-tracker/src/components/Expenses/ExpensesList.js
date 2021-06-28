import React from "react";
import ExpenseItem from "./ExpenseItem";

import "./ExpenseItem.css";

const ExpensesList = (props) => {
    /** Filter Content **/
    if (props.items.length === 0) {
        return <h2 className="expenses-list__fallback">Found No Expenses</h2>;
    }

    return (
        <ul className="expenses-list">
            {props.items.map((item, index) => (
                <ExpenseItem
                    title={item.title}
                    amount={item.amount}
                    date={item.date}
                    key={item.id}
                />
            ))}
        </ul>
    );
};

export default ExpensesList;
