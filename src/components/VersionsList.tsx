import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function VersionsList({
    versions,
    baseLink
}) {
    const [cards, setCards] = useState(versions);
    const navigate = useNavigate();

    return (
        <div style={{ display: "flex", justifyContent: "end", width: "90%" }}>
            {cards && cards.length > 0 && <div style={{
                position: 'relative',
                width: '70px',
                height: '70px',
            }}>
                {cards.map((card, index) => (
                    <div
                        key={card.id}
                        style={{
                            position: 'absolute',
                            width: '100%',
                            height: '100%',
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            top: 0,
                            left: 0,
                            backgroundColor: '#fff',
                            border: '1px solid #ccc',
                            borderRadius: '10px',
                            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                            transformOrigin: 'top right',
                            transition: 'transform 0.3s ease, zIndex 0.3s ease',
                            cursor: 'pointer',
                            zIndex: cards.length - index,
                            transform: index === 0 ? 'translate(0, 0)' : 'translate(20px, -20px)',
                        }}
                        onClick={() => {
                            if (index == 0) {
                                const clickedCard = cards[index];
                                navigate(baseLink + clickedCard.link);
                            } else {
                                const newCards = [...cards];
                                const first = newCards.shift();
                                newCards.push(first);
                                setCards(newCards);
                            }

                        }}
                    >
                        {card.name}
                    </div>
                ))}
            </div>
            }
        </div>
    );
}

export default VersionsList;
