
export default function QuestionInput() {
    return (
        <div className="searchInputContainer">
            <input
            type="text"
            className="searchInput"
            placeholder="Ask a question..."
            />
            <button className="bubble-button searchButton">
            Go
            </button>
        </div>
    )
}