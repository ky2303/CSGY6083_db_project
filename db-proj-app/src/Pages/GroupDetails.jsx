import { useNavigate, useParams, Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

var host = 'localhost'
var deployed = false
if (deployed) { host = '' };

const GroupDetails = () => {
    const [group, setGroup] = useState([]);
    const navigate = useNavigate();
    const { slug } = useParams();

    useEffect(() => {
        fetch(`http://${host}:8000/groups/${slug}`)
          .then(response => response.json())
          .then(group => setGroup(group));
      }, []);
    
    // GROUP
    //   id: int = Field(primary_key=True)
    //   name: str = Field(nullable=False)
    //   url: str = Field(nullable=False)
    //   associated_groups: Optional[str] = None
    //   description: Optional[str] = None
    //   techniques_used: Optional[str] = None
    //   techniques_used_ids: Optional[str] = None
    //   software: Optional[str] = None
    return ( 
        <>
            <div>
                <h1>{group.name}</h1>
                <table>
                    <tr>
                        <td>ID: </td><td>{group.id}</td>
                    </tr>
                    <tr>
                        <td>Group Name:</td><td>{group.name}</td>
                    </tr>
                    <tr>
                        <td>URL: </td><td>{group.url}</td>
                    </tr>
                    <tr>
                        <td>Associated Groups: </td><td>{group.associated_groups}</td>
                    </tr>
                    <tr>
                        <td>Description: </td><td>{group.description}</td>
                    </tr>
                    <tr>
                        <td>Techniques Used: </td><td>{group.techniques_used}</td>
                    </tr>
                    <tr>
                        <td>Techniques Used Ids: </td><td>{group.techniques_used_ids}</td>
                    </tr>
                    <tr>
                        <td>Software: </td><td>{group.software}</td>
                    </tr>
                </table>

            </div>
        </>
    );
};

export default GroupDetails;