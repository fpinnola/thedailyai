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
                padding: '0px 5px 0px 5px',
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