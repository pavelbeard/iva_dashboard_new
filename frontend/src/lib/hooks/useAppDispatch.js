import { useDispatch } from "react-redux";

export default function useAppDispatch() {
  const dispatch = useDispatch();
  return dispatch;
}
