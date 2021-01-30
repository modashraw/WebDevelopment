import React, { useState } from 'react';

const Slides = ({ slides }) => {
    const [ index, setIndex ] = useState(0);
    const [restartBtn, doRestart] = useState(true);
    const [prevBtn, doPrev] = useState(true);
    const [nextBtn, doNext] = useState(false);

    const carousalRestart = () => {
        setIndex(0)
        doRestart(true)
        doPrev(true)
        doNext(false)
    }
    const carousalNext = () => {
        if ((index + 1) < slides.length) {
            setIndex(index + 1)
            doRestart(false)
            doPrev(false)
            doNext(false)
        } else {
            doNext(true)
            doRestart(false)
            doPrev(false)
        }
    }
    const carousalPrev = () => {
        if ((index - 1) >= 0) {
            setIndex(index - 1)
            doRestart(false)
            doPrev(false)
            doNext(false)
        } else {
            doPrev(true)
            doRestart(true)
        }
    }

    return (
        <div>
            <div id="navigation" className="text-center">
                <button data-testid="button-restart" className={`small ${restartBtn && "outlined"}`} onClick={carousalRestart}>Restart</button>
                <button data-testid="button-prev" className={`small ${prevBtn && "outlined"}`} onClick={carousalPrev}>Prev</button>
                <button data-testid="button-next" className={`small ${nextBtn && "outlined"}`} onClick={carousalNext}>Next</button>
            </div>
            <div id="slide" className="card text-center">
                <h1 data-testid="title">{slides[index].title}</h1>
                <p data-testid="text">{slides[index].text}</p>
            </div>
        </div>
    );
}
export default Slides;
