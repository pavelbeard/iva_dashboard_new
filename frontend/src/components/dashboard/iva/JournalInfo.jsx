import { parseInfo } from "./journalFunctions";

const JournalInfo = ({ object }) => {
  return <div>{parseInfo(object)}</div>;
};

export default JournalInfo;
