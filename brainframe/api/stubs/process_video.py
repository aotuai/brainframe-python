from typing import Dict, List, Optional

import json

from brainframe.api.bf_codecs import AiIntervalType
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class ProcessVideoStubMixIn(BaseStub):
    """Provides stubs to call APIs for processing video"""

    def set_process_video(self, stream_id,
                      storage_uri: str,
                      ai_interval_type: AiIntervalType,
                      ai_interval_val: float,
                      timeout=DEFAULT_TIMEOUT) \
            -> Optional[int]:
        """Start a offline video analysis.

        :param stream_id: Stream configuration id, which can be personalized based 
            on the stream to which the video file belongs Configuration. 
            For video files belonging to this stream, the same rules can be 
            applied for analysis.
        :param storage_uri: URL where the offline video is stored.
        :param ai_interval_type: Frame fetching mode, AiIntervalType.TIME or AiIntervalType.FRAME
        :param ai_interval_val: value of this will depend on ai_interval_type.
            When interval_type is AiIntervalType.TIME,interval_val is the number of seconds (floating-point) elapsed.
            If interval_val==0, then AI analysis is performed on all frames.
            When interval_type is AiIntervalType.FRAME, it is the number of frames between. Common values are:
            1: Indicates AI analysis for all frames.
            2: means taking 1 frame every 2 frames for AI analysis.
            3: indicates that one frame is taken every three frames for AI analysis.
        :param Timeout (seconds): If the maximum concurrency of the system is insufficient, 
            wait until the timeout or normal Processing.
        :return: session_id: Transaction number, a unique ID for this analysis.
        """
        req = f"/api/process_video"

        params = {
            "stream_id": stream_id,
            "storage_uri": storage_uri,
            "ai_interval_type": ai_interval_type.value,
            "ai_interval_val": ai_interval_val,
            "timeout": timeout,
        }
        params = json.dumps(params)
        
        data = self._post_json(req, timeout, params.encode("utf-8"))
        
        if data:
            if data["resp_code"] == 200:
                return data["session_id"]
        return None

    def delete_process_video(self, session_id: Optional[int] = None, timeout=DEFAULT_TIMEOUT):
        """Delete video analysis transactions.

        :param session_id: Transaction number, a unique ID for this analysis. If session_id is None,
            it is a request removes any existing analysis transactions.
        """
        if session_id is None:
            req = r"/api/process_video" 
        else:
            req = f"/api/process_video/{session_id}"
            
        self._delete(req, timeout)
         
