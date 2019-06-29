import { MarkResult } from "../../store/mark/types";

export const getErrorMessage = (markResult: MarkResult) => {
    switch (markResult) {
        case MarkResult.SUCCESS:
            return undefined;
        case MarkResult.RESOURCE_EXPIRES:
            return "operation is expired, please try next batch.";
        default:
            return "error, please try next batch.";
    }
};