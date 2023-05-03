import {parseInfo} from "./journalFunctions";

const JournalInfo = ({object}) => {

    const parseInfoJSX = () => {
        try {
            if(object.blockReason === null)
                object.blockReason = ""

            return parseInfo(object);
        } catch (err) {
            return "parseError";
        }
    }

    return (
        <div>
            {parseInfoJSX()}
        </div>
    );
};

export default JournalInfo;