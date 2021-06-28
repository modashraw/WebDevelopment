import React, { useState } from "react";
import "./ExpenseForm.css";

const ExpenseForm = (props) => {
    //@@ title state
    const [expenseTitle, changeExpenseTitle] = useState("");

    //@@ amount state
    const [expenseAmount, changeExpenseAmount] = useState("");

    //@@ expense state
    const [expenseDate, changeExpenseDate] = useState("");

    // const [userExpenseInput, setUserExpenseInput] = useState({
    //     expenseTitle: "",
    //     expenseAmount: "",
    //     expenseDate: "",
    // });

    const titleChangeHandler = (event) => {
        // setUserExpenseInput((prevState) => {
        //     return {
        //         ...prevState,
        //         expenseTitle: event.target.value,
        //     };
        // });
        // console.log(userExpenseInput);
        changeExpenseTitle(event.target.value);
    };
    const amountChangeHandler = (event) => {
        // setUserExpenseInput((prevState) => {
        //     return {
        //         ...prevState,
        //         expenseAmount: event.target.value,
        //     };
        // });
        // console.log(userExpenseInput);
        changeExpenseAmount(event.target.value);
    };
    const dateChangeHandler = (event) => {
        // setUserExpenseInput((prevState) => {
        //     return {
        //         ...prevState,
        //         expenseDate: event.target.value,
        //     };
        // });
        // console.log(userExpenseInput);
        changeExpenseDate(event.target.value);
    };

    const submitHandler = (event) => {
        event.preventDefault();
        const expensItem = {
            title: expenseTitle,
            amount: expenseAmount,
            date: new Date(expenseDate),
        };
        props.onSaveExpenseData(expensItem);
        changeExpenseTitle("");
        changeExpenseAmount("");
        changeExpenseDate("");
    };

    return (
        <form onSubmit={submitHandler}>
            <div className="new-expense__controls">
                <div className="new-expense__control">
                    <label>Title</label>
                    <input
                        type="text"
                        value={expenseTitle}
                        onChange={titleChangeHandler}
                    />
                </div>
                <div className="new-expense__control">
                    <label>Amount</label>
                    <input
                        type="number"
                        min="0.01"
                        step="0.01"
                        value={expenseAmount}
                        onChange={amountChangeHandler}
                    />
                </div>
                <div className="new-expense__control">
                    <label>Date</label>
                    <input
                        type="date"
                        min="2019-01-01"
                        max="2022-12-31"
                        value={expenseDate}
                        onChange={dateChangeHandler}
                    />
                </div>
            </div>
            <div className="new-expense__actions">
                <button type="button" onClick={props.onCancelEditing}>
                    Cancel
                </button>
                <button>Add Expense</button>
            </div>
        </form>
    );
};

export default ExpenseForm;
