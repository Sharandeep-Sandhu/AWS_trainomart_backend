"use client";
import gsap from "gsap";
import Image from "next/image";
import Link from "next/link";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
export default function HeroFour() {
  const router = useRouter();
  const handleSubmit = (e) => {
    e.preventDefault();
  };
  useEffect(() => {
    const parallaxIt = () => {
      const target = document.querySelectorAll(".js-mouse-move-container");

      target.forEach((container) => {
        const targets = container.querySelectorAll(".js-mouse-move");

        targets.forEach((el) => {
          const movement = el.getAttribute("data-move");

          document.addEventListener("mousemove", (e) => {
            const relX = e.pageX - container.offsetLeft;
            const relY = e.pageY - container.offsetTop;

            gsap.to(el, {
              x:
                ((relX - container.offsetWidth / 2) / container.offsetWidth) *
                Number(movement),
              y:
                ((relY - container.offsetHeight / 2) / container.offsetHeight) *
                Number(movement),
              duration: 0.2,
            });
          });
        });
      });
    };

    parallaxIt();
  }, []);
  return (
    <section className="masthead -type-3 bg-light-6 js-mouse-move-container">
      <div className="container">
        <div className="row y-gap-30 items-center justify-center">
          <div
            className="col-xl-7 col-lg-11 relative z-5"
            data-aos="fade-up"
            data-aos-delay="500"
          >
            <div className="masthead__content pl-32 lg:pl-0">
              <h1 className="masthead__title">
                Your Pursuit of <span className="text-purple-1">IT Excellence</span> starts here -
                
              </h1>

              <p className="masthead__text text-17 text-dark-1 mt-25">
                A Technical Training Solutions Company providing Instructors and 
                <br className="lg:d-none" />
                delivering Tech Courses at affordable prices.
              </p>

              <div className="masthead-search mt-30">
                <div className="masthead-search__form">
                  <form onSubmit={handleSubmit}>
                    <input
                      required
                      type="text"
                      placeholder="What do you want to learn today?"
                    />

                    <button
                      className="button -purple-1 text-white"
                      onClick={() => router.push("/courses-list-2")}
                    >
                      <i className="icon icon-search"></i>
                    </button>
                  </form>
                </div>

                <div className="masthead-search__searches mt-40">
                  <p>Trending Search: az900, azure devops certification, ethical hacking course, </p>
                  
                </div>
              </div>
            </div>
          </div>

          <div
            className="col-xl-5 col-lg-7 relative z-2"
            data-aos="fade-up"
            data-aos-delay="750"
          >
            <div className="masthead-image">
              <div className="masthead-image__img1">
                <div className="masthead-image__shape xl:d-none">
                  <Image
                    width={800}
                    height={800}
                    src="/assets/img/Home/masthead/shape.svg"
                    alt="image"
                  />
                </div>
                <Image
                  width={587}
                  height={656}
                  data-move="20"
                  className="js-mouse-move"
                  src="/assets/img/Home/masthead/1.png"
                  alt="image"
                />
              </div>

              <div className="masthead-image__el1">
                <div
                  data-move="40"
                  className="lg:d-none img-el -w-250 px-20 py-20 d-flex items-center bg-white rounded-8 js-mouse-move"
                >
                  <div className="size-50 d-flex justify-center items-center bg-red-2 rounded-full">
                    <Image
                      width={24}
                      height={23}
                      src="/assets/img/masthead/1.svg"
                      alt="icon"
                    />
                  </div>
                  <div className="ml-20">
                    <div className="text-orange-1 text-16 fw-500 lh-1">
                      550 +
                    </div>
                    <div className="mt-3">Technical Courses</div>
                  </div>
                </div>
              </div>

              <div className="masthead-image__el2">
                <div
                  data-move="40"
                  className="shadow-4 img-el -w-260 px-40 py-20 d-flex items-center bg-white rounded-8 js-mouse-move"
                >
                  <div className="img-el__side">
                    <div className="size-50 d-flex justify-center items-center bg-dark-1 rounded-full">
                      <Image
                        width={20}
                        height={27}
                        src="/assets/img/masthead/2.svg"
                        alt="icon"
                      />
                    </div>
                  </div>
                  <div className="">
                    <div className="text-purple-1 text-16 fw-500 lh-1">
                      Congrats!
                    </div>
                    <div className="mt-3">Your Admission is Completed</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
