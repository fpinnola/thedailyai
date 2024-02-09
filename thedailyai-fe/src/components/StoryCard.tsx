import PagedTextViewer from "./PagedTextViewer";


const StoryCard = ({ title, summary }: { title: string, summary: string } ) => {

    return (
        <div className="slider-children">
            <div style={{
                justifyContent: 'center',
                alignItems: 'center',
                display: 'flex',
                height: '100%',
                flexDirection: 'column',
                padding: '5px 5px 10px 10px'
            }}>
                <h4>{title}</h4>
                <PagedTextViewer text={summary} charsPerPage={900} />
                {/* <p>{truncateText(summary)}</p> */}
                {/* <QuestionInput /> */}
                {/* <button style={{
                    backgroundColor: '#afafaf'
                 }}>Read more</button> */}
            </div>
        </div>
    )

}

export default StoryCard;