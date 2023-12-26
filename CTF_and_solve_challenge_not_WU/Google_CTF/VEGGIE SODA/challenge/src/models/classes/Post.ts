// @ts-ignore  
import { toDeserialize, toSerialize, } from "https://deno.land/x/superserial/mod.ts";
// @ts-ignore  
import { escape } from "https://deno.land/std@0.192.0/html/mod.ts";
import Message from '../interfaces/Message.ts';
import User from "./User.ts";

export default class Post implements Message {
    id: string;
    userId: string;
    public date: Date;
    public content: string;

    public constructor(
        content: string,
        userId: string,
        id?: string,
    ) { 
        if (id){
            this.id = id;
        } else {
            this.id = crypto.randomUUID();
        }
        
        this.userId = userId;
        this.content = content;
        this.date = new Date();
    }

    public assign(userId): void {
        if (!this.userId) {
            this.userId = userId;
        }
    }

    resolveUser(user: User){
        this.assign(user.getId());
        user.pushToPost(this);
    }

    //construct random content
    apply(user: User){
        if (!user){
            return;
        }
        const placeholders = ["Vegetables!", "I love veggies :3", "drink ur vegetables", "vigetabvlwe", "Consume VEGETABLE"];
        this.content = placeholders[Math.floor(Math.random() * placeholders.length)];
        this.resolveUser(user);
    }

    static resolve<P extends Post>(post: P, user?: User, content?: string){
        try {
            if (content){
                post.content = escape(content);
                if (user){
                    post.resolveUser(user);
                }
                return;
            }
            post.apply(user);
        } catch {
            return;
        }
        
    } 

    giveContent(): string {
        return this.content;
    }

    /* LOG GENERATION */
    validate(u: User): boolean {
        if (this.userId == u.getId()){
            return true;
        } return false;
    }

    dispatch(): string {
        return `POST GENERATED BY ${this.userId}: 
                    -- CONTENT: ${this.content}
                    -- ID: ${this.id}`;
    }

    [toSerialize]() {
        return {
          id: this.id,
          date: this.date,
          content: this.content
        };
    }

    [toDeserialize](
        value: {
          id: string;
          userId: string;
          date: Date;
          content: string;
        },
      ) {
        this.id = value.id;
        this.date = value.date;
        this.userId = value.userId;
        this.content = value.content;
    }
}
