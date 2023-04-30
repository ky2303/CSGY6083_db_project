import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

var deployed = true
var localhost = 'localhost'

if (deployed) { localhost = "127.0.0.1" };

const Report = () => {

    const [topGroups, setTopGroups] = useState([]);

    useEffect(() => {
        fetch(`http://${localhost}:8000/report/top_groups?lim=3`)
          .then(response => response.json())
          .then(topGroups => setTopGroups(topGroups));
      }, []);

    return ( 
        <>
            <div>
                <h1>Top 3 Groups</h1>
                <table>
                    <thead>
                        <tr>
                        <th align="left">Group</th>
                        <th align="left">Items in DB</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(topGroups).sort((a,b) => b[1] - a[1]).map(([key, value]) => (
                        <tr key={key}>
                            <td><a href={`/groups/${key}`}>{value[0]}</a></td>
                            <td>{value[1]}</td>
                        </tr>
                        ))}
                    </tbody>
                </table>
                <h1>Top 3 Tactics</h1>

                <h1>Top 3 Techniques</h1>

            </div>
        </>
    );
};

export default Report;