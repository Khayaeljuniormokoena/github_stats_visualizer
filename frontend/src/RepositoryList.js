import React from 'react';

function RepositoryList({ repos }) {
    return (
        <ul className="list">
            {repos.map(repo => (
                <li key={repo.id} className="item">{repo.name}</li>
            ))}
        </ul>
    );
}

export default RepositoryList;
