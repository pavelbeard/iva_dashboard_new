import {parseInfo} from "./journalFunctions";

const JournalInfo = ({object}) => {

    return (
        <div>
            {object ? parseInfo(object) : "unknown"}
        </div>
    );
};

export default JournalInfo;