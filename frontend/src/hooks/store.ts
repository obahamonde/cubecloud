import { defineStore, acceptHMRUpdate } from "pinia";
import { Message, Notify, User } from "./types";

export const useStore = defineStore("state", () => {
  const state = reactive({
    messages: [] as Message[],
    user: null as User | null,
    notifications: [] as Notify[]
  });
  const setState = (newState: any) => {
    Object.assign(state, newState);
  };

  const notify = (noti:Notify)=>{
    state.notifications.push(noti)
    const audio = new Audio(`/audio/${noti.status}.mp3`)
    audio.play()
    setTimeout(()=>{
        state.notifications.pop()
    }, 5000)
}

  return {
    state,
    setState,
    notify
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStore, import.meta.hot));
}
