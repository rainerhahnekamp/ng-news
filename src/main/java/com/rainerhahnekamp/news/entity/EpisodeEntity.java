package com.rainerhahnekamp.news.entity;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.RequiredArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
import java.util.Date;


@Data
@Entity
@EqualsAndHashCode(of = "Id")
@RequiredArgsConstructor
@Table(name = "Episode")
public class EpisodeEntity {
    @Id
    @GeneratedValue
    private Long Id;
    private String name;
    private Date publishedDate;
    private String content;
    private String imageSrc;

}