

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
                <p>{summary}</p>
            </div>
        </div>
    )

}

export default StoryCard;