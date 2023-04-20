import {parseInfo} from "./journalFunctions";

const JournalInfo = ({object}) => {

    const parseInfoJSX = () => {
        try {
            return parseInfo(object);
        } catch (err) {
            return "unknown";
        }
    }

    return (
        <div>
            {parseInfoJSX()}
        </div>
    );
};

export default JournalInfo;