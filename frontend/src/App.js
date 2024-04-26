import React, { useEffect, useState } from 'react';
import './App.css';
import LoadingIndicator from './LoadingIndicator';
import ErrorComponent from './ErrorComponent';
import RepositoryList from './RepositoryList';
import { useTranslation } from 'react-i18next';

function App() {
    const [repos, setRepos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { t } = useTranslation();

    useEffect(() => {
        setLoading(true);
        fetch('http://localhost:5000/api/repos/username')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setRepos(data);
                setLoading(false);
            })
            .catch(error => setError(error.message));
    }, []);

    return (
        <div className="container">
            <h1 className="title">GitHub Repositories</h1>
            {loading ? (
                <LoadingIndicator />
            ) : error ? (
                <ErrorComponent message={error} />
            ) : (
                <RepositoryList repos={repos} />
            )}
        </div>
    );
}

export default App;
